# S7 ходит по кругу: финиш аналитика отказывает приёмке S6 по полям, которых нет в его форме, а дирижёр без конца возвращает аналитику разбор с причиной `tooling`

id: — | кучка: `live-run-fvf` | от: живой прогон LR2-1 (плечо `factory`, релиз 0.11.0 + FV1-1 + t-180 + t-186), 12–13.11.2026 | приоритет: П1 | кандидат наверх: да

## Что не так

S7 после S6 (18 прошли, 1 упал; TC-005 красный). Аналитик `S7-qa-failure-analyst-1` (23:33) верно назвал TC-005 `TEST_BUG`
(у двух гостей общая cookie: `newContext` наследует `storageState` конфига, `core/clients/cartClient.ts:29`; контроль
`evidence/analyst-s7-2-control-two-fresh-guests.txt`) и отдал ремонт автору. Дальше круг:

1. `stage_done.py` не записывает приёмку S6 из формы аналитика: «a reject needs failure_class, one of spec, capability, data,
   tooling (got None); … a reject needs a quote: the critic's words from the artifact, with its path» (`state/conductor.jsonl`,
   22:51, 23:15, 23:45 UTC). В форме `work/handoffs/S7-qa-failure-analyst-N.yaml` полей `failure_class` и `quote` нет: в шапке
   только `verdict: concerns`, дальше `scope`/`repairs`/`not_for_repair`. Требование проверки не доходит до роли в её полях
   (FR-38, FR-11, AR-10).
2. Дирижёр трижды выбрал `rework_stage` S7 → qa-failure-analyst, `--cases TC-005 --cause tooling` (первый раз `mechanical`
   отказан). Причина `tooling` лимит не тратит, поэтому круг сам не кончается (аналитики 2, 3, 4: 23:53, 00:13, 00:37
   местного; ~35 мин и $0.3–1.3 на круг). Аналитик каждый раз пишет тот же TEST_BUG, ремонт автора не идёт: аналитик-3 — «repair
   not applied (cartClient.ts:29), round 2 of 2 spent, not_fixed». Дирижёр не разобрался сам (P22): текст отказа называет поля
   формы, а не инструмент, и повтор той же роли его не меняет.
3. Четвёртый отказ (00:57) уже другой: «the stage critic's form … does not say which dispatch of qa-runner it reviewed: the LAST
   `inputs_read` row naming a qa-runner dispatch must be `path: work/handoffs/S6-qa-runner-2.yaml`». В форме аналитика-4
   `inputs_read` — две строки `work/run-report.json`, строки формы раннера нет: её пишет код при сборке формы, а не роль
   (FR-15: путь, нужный роли, даётся ей). Вопрос дирижёра ушёл человеку.

Плечо остановлено по слову владельца (13.11 ≈ 01:00, потолок RUN-INSTRUCTIONS §5: третий повтор на одном месте). Исход плеча:
S0–S6 пройдены, S7 не закрыт, гейт B не достигнут.

## Что сделать (предложение оператора)

1. Форма S7 несёт поля, которые проверяет приёмка S6 при отказе (`failure_class`, `quote` с путём), или приёмка S6 из формы S7
   строит их из того, что форма уже говорит (`repairs[].verdict` TEST_BUG → класс, `repairs[].evidence` → путь цитаты);
   одно из двух, и читатель с писателем в одном коммите (AR-22, ось 28).
2. Строку `inputs_read` с формой проверенного dispatch раннера пишет код при сборке формы (`Reviewed dispatch:` брифа уже знает
   id), роль её не набирает.
3. Дирижёр не повторяет ту же роль с той же причиной после того же отказа: второй одинаковый отказ на одной границе — вопрос
   человеку с ценой или другой ход (rework автора S5 по TEST_BUG), не третий круг. Счётчик кругов `tooling` на границе —
   данные контроллера, решение — дирижёра (P27).
Тест: S7-форма с `repairs[0].verdict: TEST_BUG` → `stage_done` записывает приёмку S6 с классом и цитатой; два одинаковых отказа
подряд на S7 → третий `rework_stage` той же роли с той же причиной не регистрируется без слова человека.

Свидетели: `runs/factory-40.log` (23:07–00:57); `state/conductor.jsonl`, `state/driver-runs.jsonl`,
`work/handoffs/S7-qa-failure-analyst-{1..4}.yaml`, `work/digests/S7-qa-failure-analyst-{1..4}.txt`,
`state/driver-question-details.md` копии плеча.

Принципы и правила: P22, P27; FR-11, FR-15, FR-38, FR-48; AR-10, AR-17, AR-22.

Решение владельца нужно: нет.
