# «Нет функции — это пробел» записано как пропуск плана и снятие окружения, а не как продуктовый пробел

id: — | кучка: `release-next` | от: прогон LOCAL-1, разборы t-1671 Н-7 (БОЛЬШАЯ) и t-1672 П-19 (МАЛАЯ), 02.11.2026 | приоритет: П1 | кандидат наверх: нет

Сокращения: `A` = `mybooks-stand/test-automation-framework/qa-factory/artifacts/LOCAL-1`.
Разборы: `docs/tasks/specs/reviews/t-1671-local-1-gates-vs-analysis.md` (Н-7), `docs/tasks/specs/reviews/t-1672-local-1-whole-run.md` (П-19).

## Что наблюдалось

- Человек на Q4 (быстрый просмотр, XPANBFLFA-160): «quick view не реализован — занести пробелом в отчёт» (`A/state/words/gate-a-answer-1.txt:3`).
- Запись: `A/state/words/gate-a-decision.txt:16` → `case_environment-2: accept…` (waiver окружения).
- Отчёт: `A/test-report.md:156,288` — «Skipped by the plan», причина «owner's answer leaves no … path», результат `deferred`; счёт «2 deferred by your decision» (`:6`). Не продуктовый пробел (FR-21), в причине вердикта этого нет.
- Эталон ставит именно этот вопрос: `experiments/mybooks/add-to-cart-cases.md:47`.

## Причина

Слово «нет функции — пробел» разбирается как waiver окружения (`case_environment-*`), а не как пробел продукта по требованию R-23: оно идёт по ветке «пропуск плана» и не доходит до контура FR-21.

## Класс

Нереализованная функция по требованию, названная человеком пробелом, не идёт по FR-21 и не доезжает до отчёта под своим владельцем — продуктом (FR-21, FR-8, AR-27). Фабричный класс.

## Что именно менять

Направление выбрано (Lead, 02.11.2026): слово «нет функции» → строка пробела продукта по требованию.

1. **Разбор слова.** `scripts/gate_brief.py` (форма ответа на карточку case_environment/«no implementation or observable») и `scripts/stage_done.py` (запись `gate-a-decision`): вариант «функции нет — пробел» записывает у требования исход `product_gap` (не waiver окружения); waiver окружения остаётся для «стенд не может». Тест: ответ «пробел» на карточку TS-23 → требование R-23 получает `product_gap`.
2. **Отчёт.** `scripts/report_facts.py` (`## Skipped by the plan`, `:3067`) не показывает такую строку; она идёт в блок продуктовых пробелов с причиной «функции нет по требованию R-23» и владельцем product (`references/delivery-reason-owners.json`). Тест: отчёт на фикстуре содержит строку в блоке пробелов продукта.
3. **Вердикт.** `scripts/delivery_verdict.py` / `scripts/check_delivery.py`: продуктовый пробел по FR-21 блокирует `delivery_ready: yes` и входит в причину вердикта (см. RN1-16 о порядке причин). Тест: вердикт на фикстуре называет R-23.

## Принципы и правила

P20, P21; FR-8, FR-19, FR-21; AR-27.

## Связи

- RN1-16 (порядок причин вердикта), RN1-12 (кандидаты в баги), `report-delivery/findings/20261031-probely-pokrytiya-i-instrumentov-pokazany-kak-produktovye.md` (обратная сторона).
- Разборы t-1671 Н-7, t-1672 П-19.

Решение владельца нужно: нет.
