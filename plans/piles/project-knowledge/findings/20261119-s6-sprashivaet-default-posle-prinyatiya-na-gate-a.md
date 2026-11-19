# S6 снова спрашивает учётку `default` после принятия на gate A

id: — | кучка: `project-knowledge` | от: билдер t-1581 (PK2-6a), замер 19.11.2026 | приоритет: П2 | кандидат наверх: нет

Решение владельца нужно: нет — решает Lead при спеке узла.

## Что наблюдалось

Человек на gate A принимает карточку входа учёткой стенда по умолчанию (дорога 2, `check_s5_credentials`; после PK2-6a — одна общая
карточка) при отсутствующих ключах. На S6 `Driver.stand_login_problem` (`ai-packages/qa-factory/scripts/driver_stage_s6.py:1014`)
снова читает ключи учётки по умолчанию, а вызывающий (~:1193-1206) пропускает только слово
`waiver.split_overridden([STAND_LOGIN_BLOCK], pipeline, "S6")`, где `STAND_LOGIN_BLOCK` = `waiver.STAND_LOGIN_MISSING_BLOCK`
(«stand login missing»). Принятие gate A пишет другой блок («the stand's default account»). Замер билдера:
`split_overridden(["stand login missing"], {stage_overrides: [{stage: S5|S6, match: "the stand's default account", decision: ok}]}, "S6")`
→ `(['stand login missing'], [])` — блок не снят. Итог: второй вопрос на S6 для любого экранного кейса.

## Что именно менять

Класс: одно решение человека — одна запись, которую читают все места (AR-13, «решено один раз»). Нужно решить, что S6 делает после
принятия на gate A: (a) принятие gate A снимает и блок S6 (кейсы, которым нужен вход, уходят «не выполнены» с причиной, не вопрос);
(b) S6 спрашивает снова, но называет прошлое принятие. Сначала дизайн: что видит человек в отчёте в обоих вариантах. Тест: строка
таблицы PK2-6a «S6 still asks after the accept (known, finding PK2-6-s6)» переворачивается этим узлом.

Принципы и правила: AR-13, AR-19, AR-28; FR-59.
