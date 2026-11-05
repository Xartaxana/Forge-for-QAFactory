# Строка риска `s5_integrations` в `report-risk-words.json` не имеет теста: `test_report_facts.py` не называет это слово

id: — | кучка: `gates-and-words` | от: Lead пачки hotfix-12586/1 (dev2), 23.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так: узел HF1-10 (fix-round t-067, пункт 2) добавил в `references/report-risk-words.json` строку `project_wide_checks.s5_integrations`
(`references/report-risk-words.json:17`), чтобы отчёт перечислял новое слово гейта A так же, как `s5_environment`. В
`scripts/tests/test_report_facts.py` слово `s5_integrations` не встречается ни разу (`grep -c` = 0); тест упражняет только
`s5_environment` (`:106`, `:571`, `:610`). Мутация «строка удалена» ни одним ключом не убивается: если строку потеряют, слово гейта A
попадёт в отчёт без объяснения.

Свидетель: `docs/tasks/handoffs/t-067-hf1-10-fix-round.md`, «Item 2 — HF1-9 risk-words row» («`test_report_facts.py` has NO key that names
`s5_integrations` ... so the mutation "row removed" has no killing key today; a key belongs in `test_report_facts.py` (not in
`owns`) — queue it»); контрольный прогон билдера: `report_facts._gate_a` со строкой `5. s5_integrations-1, keys - accept.` возвращает
находку с `what` = новый текст.

Что сделать: ключ в `test_report_facts.py` по образцу `:610` для `s5_integrations` + отрицательный контроль (копия json без строки →
отчёт без пояснения → ключ красный). Заодно — один ключ-перечень: каждое слово `project_wide_checks` из `report-risk-words.json` имеет
тест (класс: строка данных без читателя-теста).

Принципы и правила: FR-28, FR-32, AR-22.

Решение владельца нужно: нет.
