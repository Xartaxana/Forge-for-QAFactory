# Хвосты RD1-4 по тексту и карте: `output_tail` без читателя, маскировка течёт, шаг 7 писаря утверждает долг как факт

id: — | кучка: `report-delivery` | от: критик t-758 (RD1-4, m-2, m-3, m-5), 02.11.2026 | приоритет: П3 | кандидат наверх: нет

## Что наблюдалось

- **m-2.** Поле `output_tail` производится в `_gate_a_gaps` (`check_delivery.py`) и едет пассивно (`stand_gaps.py --json`, `shown_gaps` в состоянии драйвера); поиск `output_tail` по пакету (md/json/py, не тесты) — только производитель и changelog (`red_sandbox.output_tail` — посторонний атрибут исключения). Читателя нет и текст дирижёра не говорит, где теперь лежит сырой хвост (AR-22). Не регресс (раньше хвост попадал на карточку человека), но обещание «для дирижёра» без носителя.
- **m-3.** `names_only` (`stand_gaps.py:46`, `_ASSIGNED_VALUE_RE`) маскирует только `NAME=value` с ЗАГЛАВНЫМ именем из трёх и более знаков. Не маскируются (проба): `api_token=abc123`, `PW=secret`, `Ab_TOKEN=x`, `Authorization: Bearer eyJ…`, `--token abc123`, `https://u:pass@host`, `"API_TOKEN": "abc123"`, `password: hunter2` — восемь форм; маскируются `API_TOKEN=abc123`, `TOKEN = abc`, `export GITLAB_TOKEN='glpat-xyz'`, `AWS_SECRET_ACCESS_KEY=…`. Направление ошибки — в утечку. Экспозиция строго уменьшилась (карточка путь уже гнала `names_only` в `gate_brief:1531`), поэтому не блок.
- **m-5.** Шаг 7 писаря (`agents/qa-doc-scribe.md`): «Each script exits 0 but `check_delivery.py`, whose word counts (step 2)» читается как описание; старый текст нёс «must». Литерал продиктован спекой K13.

## Класс

Данные сырого вывода, которые код сохраняет «для кого-то», должны иметь читателя и единую маскировку (FR-6, FR-41; AR-13, AR-22); текст обязанности не маскируется под факт (FR-37).

## Что именно менять

Направление выбрано (Lead пачки release-next/1, 02.11.2026).

1. `output_tail` — читатель: `references/conductor.md` получает одну строку «сырой хвост красного результата стенда лежит в `stand_gaps.py --json` → `output_tail`; читать его до вопроса человеку» (P22, «разбирается сам»). Размер `conductor.md` ограничен 12 000 байт, при 11 952 — строка вырезает равный объём из соседней. Тест: ключ присутствия в `test_conductor_investigates_first.py`.
2. `scripts/stand_gaps.py`, `names_only`: один помощник `mask_secrets(text)` на формы выше — имя ключа без учёта регистра и длины, содержащее `token|secret|pass|pw|key|auth|credential`; значение после `=`, `:` или в паре JSON; заголовок `Authorization:`; флаг `--token <v>`; `user:pass@` в URL. Ожидание: восемь форм выше замаскированы, четыре маскируемых прежде — тоже, обычный текст `password` без значения не меняется. Тест: `scripts/tests/test_stand_gaps*.py` — таблица 12 образцов (8 + 4) и контроль «не секрет»: слово `password` без значения и обычное предложение остаются без изменений.
3. Единственность: `gate_brief.py:1531` и `stand_gaps` зовут тот же `mask_secrets` (поиск `names_only` вне `stand_gaps.py` пуст).
4. `agents/qa-doc-scribe.md` шаг 7: «Each script must exit 0, except `check_delivery.py`, whose word counts (step 2)». Размер ≤ 9122 байт сохранён (был 9087). Тест: K13 `test_delivery_ownership.py` — литерал обновляется той же правкой.

## Принципы и правила

FR-6, FR-37, FR-41; AR-13, AR-22.

## Связи

- `docs/tasks/specs/reviews/t-758-rd1-4-diff-critic.md` (m-2, m-3, m-5); RD1-4 (`release-next/1`).

Решение владельца нужно: нет.
