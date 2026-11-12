# Критик кода S5 закрывает ревью без единой пробы чувствительности, а дирижёр говорит человеку, что фабрика пробы произвести не может

id: — | кучка: `live-run-fvf` | от: живой прогон LR2-1 (плечо `factory`, релиз 0.11.0 + FV1-1), 12.11.2026 | приоритет: П1 | кандидат наверх: да

## Что не так

S5, окно 1 (TC-001/002/004/005), `S5-qa-code-critic-2`: 13 ходов, 70 с, только статическое чтение. Все 10 экземпляров —
`unverified` («no probe run»), F-1/F-2 механические с `blocking: false`, verdict `concerns`. Код записал долг
`work/probe-debt/S5-qa-code-critic-2.json`: «the probe model file work/probe-models/S5-qa-code-critic-2.json was not written in this
window; 10 instances x their checks owed». То есть роль не начала пробы вовсе: инструмент не падал, файл модели проб (где роль
предлагает «значение сломанного продукта», P30) не написан. Своей причины роль не назвала. Бриф 20 774 B при потолке 6 144 B
«after every cut»; указание на пробы в нём есть (строки 123, 132: `probe_by_code.py` «the default probe, every check of every
new/changed test»).

Финиш отказал: окно ревью не записано (`review_receipt_ref`) и нет «sensitivity proof… and no reason for its absence» — текст
отказа сам называет команду и пишет «These are the review's own receipts, not the person's to produce». Дальше:
- `round` человека (repair_limit, «the test writer repairs what the critic rejected») ушёл не автору, а дирижёру («refusal round 2
  of 2 goes to the conductor»; `runs/factory-25.log`) — вариант не исполнен как обещан (класс FV1-13);
- дирижёр спросил человека и написал «The factory cannot produce the probes for the critic» — неправда: отказ называет
  `probe_by_code.py … (the check is live)` (P22: сначала разобраться самому; FR-48; FR-41: неизвестное — не факт).

Повторы: критики 3 и 5 окна 1 — тоже без проб (critic-3: «probe models not written; stand login probe contradicts itself»;
critic-5: «probe_by_code needs a per-check model file; not written»). Критик 6 окна 2 пробу начал: `probe_by_code.py` вернул
`not_executed` («0 of 8 checks proved», cause `tooling`), `window_record.py --review-receipt` отказал из-за отсутствия квитанций
чувствительности (`work/digests/S5-qa-code-critic-6.txt`) — инструмент проб на тестах Playwright/TS не исполняет проверку
(вероятно, тот же класс языкового исключения, что FV1-19; проверить в разборе). Пробел окна закрыт словом `not receipted` и
`debt` (по слову владельца «продолжать через пробел»).

## Что сделать (предложение оператора)

1. Разобрать, почему критик пропускает пробы (бриф втрое выше потолка — срезано? хартия? цена: «5 runs for TC-001 Then 1 alone» при
   входе ~56 с на прогон); пробы — работа критика (P27, P30), отказ от них — с записанной причиной, не молча.
2. Отказ финиша критика, у которого «review's own receipts, not the person's», идёт роли (перезапуск критика с текстом отказа), не
   человеку (FR-3, P22).
3. Дирижёр не утверждает «фабрика не может», когда текст отказа называет рабочую команду.

Свидетели: `runs/factory-24.log`, `runs/factory-25.log`; `work/probe-debt/S5-qa-code-critic-2.json`,
`work/test-code/critic-findings-S5-qa-code-critic-2.md`, `state/driver-question-details.md` копии плеча (21:52).

Принципы и правила: P22, P27, P30; FR-3, FR-41, FR-48; AR-17, AR-29.

Решение владельца нужно: нет.
