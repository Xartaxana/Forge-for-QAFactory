# S6: на интерактивной дороге диспатчится ранер, который ничего не запускает, — закрытие S6 кодом живёт только в драйвере (≈9 минут)

id: — | кучка: `execution-report` | от: прогон TP1-14857 на 0.10.5, `testproject1-dev-010`, 29–30.10.2026; разбор t-1597 §2 п. 8 и §4 N2 (`docs/tasks/specs/reviews/t-1597-14857-why-slow.md`) | приоритет: не задан разбором (предложено П2, решает Lead) | кандидат наверх: нет

## Что наблюдалось

S6 (23:59:12 → 00:10:19Z, 11,1 мин): все три кейса «reused: already run on unchanged bytes, stand and version». Ушло: `story_step start` 125 с, ранер 5,2 мин (два вызова `--mine` по 79 и 89 с, оба
ответили `reused`), `finish` 94 с. Карточка S6 (`skills/qa-story/phases/s6.md:6, 74-79`) обещает «code closes S6 itself: no runner, nothing re-run», но это закрытие есть только у драйвера:
`story_run.py:10208` с `execution_request.fresh_evidence` (`story_run.py:10268`). В `story_step.py` вызова `fresh_evidence` нет (Grep по `fresh_evidence|close_by_code|closes S6|manual_close` над
`story_step, story_run, controller, execution_request` — попадания в `story_run.py`, `execution_request.py`, `controller.py`; в `story_step.py` нет; тот же вызов находит `story_run.py:10208`).

## Корень и класс

Шаг, который есть у драйвера и которого нет у `story_step start`: «одно действие, две дороги, у одной нет шага» (AR-15; FR-17; ось «Skill phase <-> driver», B-261). Интерактивный прогон
(дирижёр — сама сессия) драйвера не использует по построению (SC2-38, «Слово владельца 29.10.2026»).

## Что нужно (t-1597 §4 N2)

1. Закрытие S6 по свежести переезжает в ОДНУ функцию, которую зовут и `story_run.py`, и `story_step start --stage S6` (AR-15). `start` отвечает «S6 closed by code: every automated test reused (…)» и
   печатает карточку S7.
2. Тот же обзор — для других закрытий кодом, живущих только в драйвере: `s7.pretriaged`, `s6.manual_close` (S7 в этом прогоне закрыл `code_only`, потому что его карточка называет команду; карточка S6
   команду не называет). Результат обзора — перечисление «есть у обеих дорог / только у драйвера» в спеке.

Края для спеки: часть кейсов свежа, часть нет (диспатч ранера только на несвежие, не закрытие); ручная половина S6 (закрытие не касается её); нет ни одного автоматизированного теста; свежесть по байтам, стенду и
версии — прежняя функция без изменений смысла.

Ожидаемая экономия: ≈9 минут на прогон, у которого S5 уже всё прогнал (11,1 → ~2 мин), и один диспатч.

Решение владельца нужно: нет.
Связи: `conductor/findings/20261015-stage-done-stiraet-code-only-s6-stoporit-vhod-v-s7.md` (то же закрытие, сторона читателя), DC1-12 (паритет ручного блока S6 скилла и драйвера), DC1-19
(`driver-controller/findings/20261030-doroga-dirizhyora-ne-zapisyvaet-otvety-cheloveka-na-voprosy-gejta.md`, тот же класс); дом по замыслу разбора — `conductor`, по коду
(`story_step.py`, `story_run.py`) — `speed-cost`, выбрано по коду, который чинится; P3, P6; FR-17, FR-51; AR-15.
