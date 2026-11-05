# Префикс `stand gap:` разбирают четыре парсера: `contract.stand_gap_id` и три собственных `startswith` (waiver, story_run ×2) — один читатель по AR-13

id: — | кучка: `driver-hosts` | от: Lead (Fable), 26.10.2026; скаут t-1237 | приоритет: П2 | кандидат наверх: нет

## Что не так / что сделать

Блок `stand gap: <id>` в `stage_overrides[].match` (префикс `STAND_GAP_MATCH_PREFIX = "stand gap:"`, `contract.py:386`) читают
четыре места, и читают по-разному:

1. **Выживший — `contract.stand_gap_id`** (`ai-packages/qa-factory/scripts/contract.py:414-420`): сворачивает пробелы,
   сравнивает без учёта регистра, срезает кавычки и обратные апострофы вокруг значения; возвращает `""`, если префикса нет.
2. `waiver.py:314-317` `is_stand_gap_block`: `_fold(match).startswith(contract.STAND_GAP_MATCH_PREFIX)` — свой разбор, только
   булево «это блок stand gap».
3. `story_run.py:13937-13941` (гейт A, `via_door`): `startswith(prefix + " ")` и срез `[len(prefix):]` — без свёртки регистра и
   без снятия кавычек; значение сверяется с `by_gap` как есть.
4. `story_run.py:14048-14050` (тот же гейт A, ветка отказа записи): вторая копия того же `startswith` и среза.

Рядом — общий `contract.prefix_value` (`contract.py:113-124`): третья реализация той же пары «префикс + один токен» (он требует
ровно один токен, `stand_gap_id` — нет; кавычки и пробелы они срезают разными наборами). `prefix_value` уже читает и этот префикс: `waiver.py:1023`
(`block_in_words`) и `test_contract.py:130` зовут его с `STAND_GAP_MATCH_PREFIX`.

**Правило.** AR-13 (`design/architecture.md:131-136`): «where the package has one reader for a file or fact, every consumer calls
it. A second parser of the same bytes is a defect even when it agrees today». Носители AR-13 называют оси 16/19/20/21 и строки
оси 5, но не этот префикс; докстринг `contract.stage_override_values` (`:127-134`) перечисляет префиксные слова AR-13
(`executor unavailable:`, `then handed:`, `probe gap:`) без `stand gap:`. Поэтому `test_one_source_per_fact.py` префикс не
называет (0 совпадений; тот же поиск находит имена в `test_contract.py` и `test_stand_gap_contract.py`, которые держат только сам
`stand_gap_id`), и расхождение (кавычки, регистр, `stand gap:TC-7` без пробела) не ловится: сайт 3 принимает
`stand gap: TC-7` и не принимает `Stand Gap: TC-7` или `stand gap: "TC-7"`, сайт 2 принимает оба, выживший — оба и значение.

**Что сделать (узел C3-29).**

- Три собственных парсера идут через `contract.stand_gap_id` или через булев двойник `contract.is_stand_gap_match` рядом с ним
  (решает дизайнер; булево — это `bool(stand_gap_id(match))` либо отдельный ответ на «префикс есть, значение пусто», дизайнер
  называет направление ошибки: пустое значение блока — не блок stand gap, а отказ с дверью, не молчаливый проход, FR-4/FR-59).
- `stand gap:` — в список AR-13 в докстринге `stage_override_values` и в носители AR-13 в `architecture.md` (имя `stand_gap_id`).
- По тесту на каждое из трёх бывших мест: вход в другом регистре, с кавычками, без пробела после двоеточия, с пустым значением.
- `contract.prefix_value` как вторая реализация — вердикт дизайнера «свести / остаётся: почему» (AR-13 говорит про те же байты).

Чем стар вопрос: старая заметка очереди «`contract.stand_gap_id` :186» устарела — на :186 стоит докстринг `then_number`;
актуальные номера — выше.

Свидетель: скаут t-1237 (26.10.2026); `ai-packages/qa-factory/scripts/contract.py:386`, `:113-124`, `:127-134`, `:414-420`;
`ai-packages/qa-factory/scripts/waiver.py:314-317`; `ai-packages/qa-factory/scripts/story_run.py:13937-13941`, `:14048-14050`;
`ai-packages/qa-factory/design/architecture.md:131-136`.

Принципы и правила: AR-13, FR-12, FR-58, P10.

Решение владельца нужно: нет.

## Куда

Строка C3-29 пачки `conductor/batch-3-vhodyashchie.md` (D-0044; пачка не взята).
