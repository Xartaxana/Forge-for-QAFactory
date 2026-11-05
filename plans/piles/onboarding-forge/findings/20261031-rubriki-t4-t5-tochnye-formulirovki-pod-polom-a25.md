# Две точные правки текста рубрики критика кода (T4 «no static detector», T5 «и сторона») не влезали в пол A25 после TQ1-3 (t-520 T4, T5)

id: — | кучка: `onboarding-forge` | от: критик t-520, T4 и T5 (`docs/tasks/specs/reviews/t-520-small-nodes-critic.md:50–51`), 31.10.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

- T4: `references/code-review-rubric.md:44` — «tautologies are yours (no detector)». Красная проба ловит `no_failure` во время прогона (`handoffs/vocabulary.yaml:125`), поэтому «no detector» преувеличивает; верно «no static detector» (`Grep tautolog` в `scripts/` пуст — статического нет). +7 B.
- T5: `references/test-code-patterns.md:24` — «A relative result (old/new, before/after, order) asserts BOTH sides against expected values and the side»: перечисление не называет `side`, а рубрика (`code-review-rubric.md:48`: «old/new, before/after, side, order») и строка реестра называют. Привести к «(old/new, before/after, side, order)». +6 B.
- Запас байт: после фикс-раунда TQ1-3 запас над полом аудита A25 (сумма четырёх слоёв ролей, `test_audit_rules.py:790`) — по слову carrier-строки (`docs/tasks/release-0.10.8.md:183`) 29 B; число 29 в отчёте критика не найдено (в отчёте стоит «free is 3 B above the floor» до фикс-раунда T1/T2). +13 B этих двух правок влезают; потолок не поднимать (AR-20).
- Копии срезов (`references/slices/qa-automator/test-code-patterns.md:23`, `references/slices/qa-code-critic/test-code-patterns.md:23`) порождаются, руками не правятся.

## Что именно менять

1. `references/code-review-rubric.md:44`: «(no detector)» → «(no static detector)».
2. `references/test-code-patterns.md:24` (и то же перечисление, если оно есть во втором месте): «(old/new, before/after, order)» → «(old/new, before/after, side, order)».
3. Срезы пересобрать существующим генератором (`scripts/contract_slices.py`; точное имя команды проверить по `--help` при взятии), без правки слайсов руками.
4. Тест: `test_audit_rules.py` A25 зелёный и запас не меньше нуля (witness, `selftest.py --limits --lang`); в пинах `test_critic_lines_hf2.py` слова «no static detector» нет и не мешает. Мутация: вернуть «no detector» — красит ключ-присутствие (добавить ключ в `test_critic_lines_hf2.py`).

## Принципы и правила

FR-54; AR-10, AR-20 (потолок не поднимается); AR-22. Связи: TQ1-3, `docs/tasks/specs/reviews/t-520-small-nodes-critic.md` T1–T3 (блокеры, чинятся фикс-раундом).

Решение владельца нужно: нет.
