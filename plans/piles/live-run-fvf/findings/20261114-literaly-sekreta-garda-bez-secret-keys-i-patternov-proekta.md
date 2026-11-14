# Набор литералов гарда секрета берёт только пароль аккаунта: значения `environment.secret_keys` и `secret_content_patterns` проекта не учтены

id: — | кучка: `live-run-fvf` | от: критик диффа FV1-28 волны 1 (`docs/tasks/specs/reviews/20261114-fv1-28-wave1-diff-critic.md`, очередь Q5) | приоритет: П2 | кандидат наверх: нет

## Что не так

Класс фабрики: **один факт («что считается секретом проекта») читают три дороги, и гард берёт одну (AR-13, AR-15)**. Спека карточки A1 предписала `read_login`, и `ai-packages/qa-factory/scripts/first_look.py::sign_in_secret_faults` (~482)
сверяет литералы пароля одного аккаунта. Уже существуют читатели большего: `ai-packages/qa-factory/scripts/machine_facts.py::secret_values` (~338: значения всех `secret_keys` проекта) и
`ai-packages/qa-factory/scripts/manual_capture.py::secret_pattern_hit` (~575: `secret_content_patterns` проекта). Реестр `environments.sign_in`, который строит карточка C1 (FV2-57), живёт дольше истории, поэтому
пропущенный секрет живёт в нём долго.

## Что именно менять

Выбранное направление: гард берёт набор литералов у существующих читателей, нового перечня не заводится; делается ДО C1 (FV2-57 — предусловие).

1. `ai-packages/qa-factory/scripts/first_look.py`: набор литералов для `sign_in_secret_faults` = пароль `read_login` + `machine_facts.secret_values(config, environ, root=…)`; тот же шаблонный проход `manual_capture.secret_pattern_hit(text, cfg)` по каждому листу.
   `secret_values` не читается (ошибка/нет конфига) — набор из пароля как сегодня и строка «the project's secret keys could not be read» в отказ-подсказке не печатается значением (FR-59: неизвестное названо, не пропуск).
2. Пусто: нет `secret_keys` или `secret_content_patterns` — как сегодня (только пароль аккаунта).
3. Тесты — строки таблицы `ai-packages/qa-factory/scripts/tests/test_first_look.py` (keep, быстрый): значение второго секрета проекта (`secret_keys`) в `sign_in` отказано; текст, подходящий `secret_content_patterns`, отказан; конфиг не читается — отказ по паролю
   работает как раньше; значение секрета не печатается в тексте отказа.
4. Порядок: после карточки A1 (FV2-54: функция существует) и ДО карточки C1 (FV2-57): Lead при взятии добавляет строку `очередь`/зависимость; строка FV2-57 этим находом не правится.

Принципы и правила: AR-13, AR-15, AR-28; FR-54, FR-59.

Связи: `findings/20261114-sekret-v-svobodnom-tekste-strok-pervogo-vzglyada.md` (та же функция, другое поле).

Решение владельца нужно: нет.
