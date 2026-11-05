# Описание бага в «Context» тикета (состояние ДО исправления) принято тестировщиком требований за требование и поднято блокером против AC

id: — | кучка: `words-gates` | от: отзыв пользователя Dev6 (TP2-2702), плагин 0.10.x, 28.10.2026 (разбор t-1553) | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Слова пользователя, как написаны: «One mismatch, it gives me back this blocker: R-3 (blocker). The ticket says reopening shows the success screen, and the code unmounts on close. a) Test AC-3 as written: a fresh empty form after a successful registration. b) Rewrite the Then to the ticket's wording, and leave it unautomated until you answer. The ticket in its context explains the situation before the fix: Context: After a successful registration, reopening the modal shows the success screen instead of a fresh form — making it impossible to start a new registration without refreshing the page. and one of the ACs describes the expected behavior: After a successful registration, reopening the modal presents a fresh empty form. I had to explain it to him what needs to be done, and later it asked once more to confirm. It must have confused the context with AC.»

Роль приняла описание дефекта «как было» за утверждение о требуемом поведении, получила «противоречие» с AC-3 и спросила человека дважды. Вопрос ложный: между состоянием до исправления и ожидаемым поведением противоречия нет, это и есть смысл багового тикета. Фабрика не угадала (P20 соблюдён), но поднятый блокер — ложный.

## Где в коде

Из разбора t-1553 (пункт 3; пути от `ai-packages/qa-factory/`; номера строк проверить по тексту при взятии):
- `agents/qa-requirements-tester.md`: источники реестра — закрытый список `story | feature | assumption | discussion | ac | derived` (строки 44-46), описание читается как `story`; матрица противоречий (строки 67-71): ячейка `contradicts` — «вопрос владельцу, не молчаливый выбор стороны»; каждая такая ячейка несёт обе цитаты (строка 128) и `verdict: blocked` для противоречия, меняющего цель или границу (строка 133).
- В тексте роли, `references/coverage-design.md`, `skills/qa-story/phases/s1.md` и `s2.md` нет указания, что описание дефекта «как сообщён» в багом тикете говорит о состоянии ДО исправления, а не о требовании. Единственная «до»-машинерия — столбец `delta` реестра и `## Behaviour claims` с `before_ref` (P20) — про утверждения о коде, не про прозу тикета.
- P23 (`PROJECT.md`): описание и AC — равные источники требований; поэтому предложение из Context встало рядом с AC-3. Правила, различающего «описание бага» и «ожидаемое поведение», нет.
- Часть «спросил второй раз, подтвердить» — FR-7 (не переспрашивать пройденную границу); путь повтора по прогону не прослежен (нужны артефакты). Родственная кучка для этой части — `gates-and-words` (пачка 1).

Ограничение вывода: прогона TP2-2702 в руках не было.

## Класс

Различие «состояние до» и «ожидаемое» в прозе тикета: бага-описание — свидетельство ДО (P20, «было ДО»), не оракул ожидаемого. Противоречие между состоянием ДО и AC — не развилка и не вопрос человеку. Не блокер: стоит одного лишнего вопроса.

## Решения владельца

Владелец, 28.10.2026: «не в 0.10.5, в пачки». Узел RC1-12: текст роли `qa-requirements-tester.md` (и, если нужно, общий слой) различает описание бага (состояние ДО) и ожидаемое поведение; расхождение между состоянием ДО и AC не поднимается как `contradicts`/блокер; проверка — тест присутствия правила в тексте роли. Решение владельца нужно: нет.

Принципы и правила: P20, P23, FR-7, FR-12, FR-47, AR-26.
