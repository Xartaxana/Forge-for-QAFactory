# Ворота относительного оракула в `s5_precheck` читают равенство только в трёх записях: assertpy и Playwright проходят молча

id: — | кучка: `execution-report` | от: обзор MR !12 по исполнению (`docs/tasks/specs/reviews/t-1644-mr12-review-execution.md`, M1 MAJOR), 01.11.2026 | приоритет: П2 | кандидат наверх: нет | узел: TQ1-30

## Что наблюдалось

- `ai-packages/qa-factory/scripts/s5_precheck.py`: `_equality_pair`, `MATCHER_WRAPPERS = ("equal_to", "is_")`, `TRIVIAL_MATCHERS`, `SHAPE_MATCHERS`, `MATCHER_CALLS` (~2032-2043, 2086-2110), `_relative_gaps`. Равенство опознаётся как голый `assert a == b`, hamcrest `assert_that(a, equal_to(b) / is_(b))` и `assertEqual`; всё прочее доходит до `if pair is None: continue` и не даёт ни находки, ни подсказки, ни заметки.
- Контрольный прогон критика (одно и то же тело теста: `before = c.get(); c.move(); after = c.get()`, токен `before` есть во всех четырёх):

| Форма assert | Результат |
|---|---|
| `assert after == before` | `[(5,'after','before')]` — поймано |
| hamcrest `assert_that(after, equal_to(before))` | `[(5,'after','before')]` — поймано |
| assertpy `assert_that(after).is_equal_to(before)` | `[]` — тихо |
| Playwright `expect(after).to_equal(before)` | `[]` — тихо |

- Инвариант ворот: «тест, чья база может быть отказом и не утверждена, не проходит выход S5 молча»; ложный проход допустим «только для сравнения без общего вызова и без токена». Здесь токен есть — допуск не применим.
- Словарь hamcrest (~40 имён) — список в коде; его близнец `baseline_names` уже лежит в `references/detectors.json`. Не BLOCK: до этого MR ворот не было, регресса нет.

## Класс

Неизвестное становится проходом (AR-28, FR-59) вне собственного допуска ворот, а закрытое разнообразие записей сравнения живёт в коде (AR-1, FR-13).

## Что именно менять

Направление выбрано (Lead пачки, 01.11.2026). Пути — от `ai-packages/qa-factory/`.

1. `references/detectors.json`: рядом со строкой `baseline_names` добавить строку `equality_spellings` — данные по библиотекам: bare `==`, `assertEqual`, hamcrest (`equal_to`, `is_`), assertpy (`is_equal_to`), Playwright (`to_equal`) и тому подобное; форма строки — как у соседней (один читатель в `s5_precheck`). `MATCHER_WRAPPERS`, `TRIVIAL_MATCHERS`, `SHAPE_MATCHERS`, `MATCHER_CALLS` в коде заменить чтением этой строки. Тест (`scripts/tests/test_s5_precheck.py`): assertpy-форма и `expect(...).to_equal(...)` из таблицы дают находку `[(5,'after','before')]` так же, как `==`.
2. `_equality_pair` / `_relative_gaps`: сравнение, которое код не смог прочесть как равенство, при наличии токена базы (`before` и т. п.) даёт заметку критику кода (в структуре подсказок/заметок, что уже использует `s5_precheck`; новую форму вывода не вводить, AR-18), а не `continue`. Направление ошибки: заметка не блокирует выход (P1: код сообщает, не останавливает), но попадает в бриф критика кода. Тест: неизвестная форма (например `verify(after).same_as(before)`) с токеном базы — заметка есть; та же форма без токена базы — заметки нет.
3. Контроль: тест на пустую строку `equality_spellings` в `detectors.json` — поведение как при отсутствии ключа: берётся встроенный минимум (`==`, `assertEqual`), заметка из п. 2 при этом срабатывает на остальные формы, а не молчание.

## Связи

- TQ1-18 (оракул «как до» на отрицательной базе) — те же ворота; TQ1-16 и TQ1-19 меняют `s5_precheck.py` (общий горячий файл: функции в `owns` диспатча).

## Принципы и правила

P1, P2, P20; FR-13, FR-59; AR-1, AR-18, AR-28.

Решение владельца нужно: нет.
