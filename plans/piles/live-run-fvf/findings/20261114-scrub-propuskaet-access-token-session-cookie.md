# Единый `scrub` пропускает `access_token=`, `session=` и `Cookie: JSESSIONID=…`, а текст отказа обещает «cookie»

id: — | кучка: `live-run-fvf` | от: критик диффа FV1-28 волны 1 (`docs/tasks/specs/reviews/20261114-fv1-28-wave1-diff-critic.md`, строка очереди Q1; эмпирика — таблица «Spelling» того же вердикта) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **один скруббер, но его перечень слов-ключей неполон (AR-1, FR-41)**. `ai-packages/qa-factory/scripts/app_card.py::scrub` (~72) заменяет значения по `_KV` (~64) с перечнем слов
`_KEYWORD` (~63: `pass…`, `pwd`, `pw`, `secret`, `token`, `api_key`, `access_key`, `private_key`, `authorization`, `credential`). Слов `cookie` и `session` нет, а `\btoken` не срабатывает после `_`, поэтому `?access_token=…`,
`?session=…`, `Cookie: JSESSIONID=…` записываются как есть (измерено критиком: секрет попал в `work/first-look.yaml`). Текст отказа первого взгляда обещает «cookie». Скруббер общий для каждого читателя карточки; направление ошибки — «лишнее
закрашивание» (безопасное).

## Что именно менять

Выбранное направление: перечень слов расширяется, по строке-тесту на форму.

1. `ai-packages/qa-factory/scripts/app_card.py` (`_KEYWORD`): добавить `access[_-]?token`, `refresh[_-]?token`, `session(?:[_-]?id)?`, `jsessionid`, `cookie`, `set-cookie`, `csrf`/`xsrf` (последние две — по решению дизайнера
   после перечня читателей: закрашивание лишнего допустимо, потеря нужного слова-имени нет, «names of keys are kept»). Значения вида `Cookie: a=1; b=2` закрашиваются целиком до конца строки заголовка.
2. Расхождение с записью Lead («данные»): `_KEYWORD` сегодня — строка кода, не строка данных; перенос перечня в данные — узел OH1-8 (`findings/20261019-odna-tablitsa-shablonov-sekretov-dlya-garda-i-redaktora.md`); этот узел НЕ ждёт его: слова дописываются
   в существующий `_KEYWORD`, а при переносе OH1-8 переезжают вместе.
3. Тесты — строки таблицы в `ai-packages/qa-factory/scripts/tests/test_app_card.py` (дизайнер сверяет имя файла по `test-layers.json`; быстрый): `access_token=X`, `?session=X`, `Cookie: JSESSIONID=X`, `Set-Cookie: a=X; Path=/`,
   в другом регистре, в URL-кодировке `%3D`, пустое значение (`session=` — ничего не закрашено, как у `token=`), значение на пределе длины и за ним; ключ остаётся виден, значение — `[not printed]`.

Принципы и правила: AR-1, AR-13, FR-41, FR-54.

Связи: OH1-8 (одна таблица шаблонов секретов; кучки `onboarding-hooks`, `words-gates`); FV2-73, FV2-74 (те же защита секрета первого взгляда).

Решение владельца нужно: нет.
