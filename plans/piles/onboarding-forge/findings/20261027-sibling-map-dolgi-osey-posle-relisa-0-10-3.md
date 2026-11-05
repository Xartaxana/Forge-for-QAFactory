# Карта `docs/SIBLING_MAP.md` должна семь пунктов (строки и две новые оси) по ревью релиза 0.10.3: правит полный Lead, файл механизма

id: — | кучка: `onboarding-forge` | от: критики релиза 0.10.3 (t-1277, t-1286, t-1296, t-1310, t-1318, t-1319, t-1320), 27.10.2026 | приоритет: П3 | кандидат наверх: нет

Что не так / что сделать: ревью узлов релиза 0.10.3 оставили строки и оси карты без носителя; строки карты — файл механизма, билдер его не правит (билдеры отдали вопрос Lead), правит полный Lead при слиянии или отдельной правкой. Правило 9 `CLAUDE.md`: новая симметрия — новая ось тем же коммитом. Список долгов с источником (номера строк — по дереву ветки узла, на `main` могут отличаться):

1. Ось 11 («shell-command recognizers»): назвать `hooklib._read_units` (`hooklib.py:1385-1396`) как единственное место построения читателя; строка карты называет `walk (+ _Reader)` как один токенайзер (на ветке 5b — `:265`). Источник: `docs/tasks/specs/reviews/t-1296-sc1-5-diff-review.md`, F-8.
2. «S5 dispatch kind» (шаг 8 B1a SC1-14): строка не написана ни на `main`, ни на ветке (grep `-i "s5 dispatch kind|s5_part_of"` — 0; контроль — строка 128 `s3_window_of`); в список сайтов добавить читателей B1b: `exit_gate._s5_plan_dispatch`, `s5_plan.mode` / `reviews`, `Controller._s5_plan_problems`. Источник: `docs/tasks/specs/reviews/t-1320-sc1-14-chain-diff-review.md`, F-9 (условие слияния; интегратор пишет коммитом слияния).
3. «Читатели строк плана» (ось секционной карты, AR-15 §1 спеки SC1-3): `PLAN_ROWS_KEYS` / `rows_of`, остаточные копии — см. находку `speed-cost/findings/20261027-chitateli-strok-plana-ostatok-q3-sc1-3.md`. Источник: `docs/tasks/specs/reviews/t-1286-sc1-3-diff-review.md`, Q-3.
4. Ось «Code-only stage closes» (`docs/SIBLING_MAP.md:124`): строка не называет `code_close_conflicts` (и после фикс-раунда `code_close_facts`) предикатом «закрываема кодом сейчас»; вместе со строкой оси 25 (свежесть прогона и пробы: читатель «контекст закрытия S6»), которую спека даёт Lead. Источник: `docs/tasks/specs/reviews/t-1277-hf3-6-diff-review.md`, раздел «Class-wide completeness» и F-1.
5. Ось 14 («один читатель транскриптов»): читатели в `experiments/` (`common.py`, `run_sinks.py`, `q9_cache_ttl.py`) не названы в строке «Queued». Источник: `docs/tasks/specs/reviews/t-1310-sc1-11-b0-diff-review.md`, Q2.
6. НОВАЯ ось «читатели формы передачи → `handoff_check.form_view`»: перечень читателей `story_step._form_halt_word`, `story_run.assemble_digest` / `conductor` / `written_outputs`, `handoff_help.main`, `repair_route.read_form` → `ledger.py:987`; детектор (пока grep по `handoff.parse(` / `H.parse(` / `handoff.load(`, кандидат в census-тест); очередь SC1-14 (`exit_gate._s5_plan_outputs_errors`, `s5_plan._review_element`); заодно строка `:131` «`14/16/33`» → «`14/16/28`». Источник: `docs/tasks/specs/reviews/t-1319-sc1-2-chain-diff-review.md`, раздел 3 и п. C-3 фикс-раунда.
7. НОВАЯ ось «выход хука, которого модель не видит» (hook → model channel): один адаптер `host_adapter.notice_output` / `context_output` ↔ все печатающие хуки; члены класса — в находке `speed-cost/findings/20261027-klass-nemogo-vyvoda-hukov-exit-0.md`. Источник: `docs/tasks/specs/reviews/t-1318-sc1-6-diff-review.md`, раздел «Класс ...» («Предлагаю Lead»; в карте существует «ось 5» только как близнецы стадий).

Что сделать: полный Lead вносит пункты 1-7 в `docs/SIBLING_MAP.md` (новая ось — вместе с детектором или явной строкой «detector: grep, очередь»). Часть пунктов ревью называет исполнимыми в слиянии или фикс-раунде своего узла (2 — «коммитом слияния», 6 — п. C-3 фикс-раунда SC1-2); перед правкой каждый пункт сверяется с `main` по grep с позитивным контролем, чтобы не вписать дважды.

Свидетель: ревью по списку выше (`docs/tasks/specs/reviews/`).

Принципы и правила: PROJECT.md (таблица «Где что лежит»: `docs/SIBLING_MAP.md`); `CLAUDE.md` правило 9 (класс — вся карта), правило 10(b) (оси перечисляются).

Решение владельца нужно: нет (файл механизма — полный Lead).
