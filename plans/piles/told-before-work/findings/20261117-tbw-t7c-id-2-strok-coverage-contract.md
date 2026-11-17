# id 2 строк `coverage_contract`

id: — | кучка: `told-before-work` | от: спека «Told before work: finish» (`docs/tasks/specs/20261117-told-before-work-finish-spec.md`), 17.11.2026 | приоритет: П1 | кандидат наверх: нет

Что не так / что сделать: Класс: требование обязательств названо в строках, сайты отказов id не несут (AR-9, AR-10).

Что именно менять: `coverage_contract.validate_obligations`: `coverage_contract:obligations` и `.observation` на сайтах; текст побайтно прежний. Функция служит и фильтром проекции — Record не меняет возвращаемое значение фильтра (строка, утверждающая сегодняшнее значение). Не трогать `manual_current`. Тест `tbw_t7c_sites`.

Карточка: `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, карточка §6 «Card T7c» — читать там, не копировать сюда.

Свидетель: спека wave0 §3b; F-W3 (a).

Принципы и правила: AR-9, AR-13, AR-29.

Решение владельца нужно: нет.
