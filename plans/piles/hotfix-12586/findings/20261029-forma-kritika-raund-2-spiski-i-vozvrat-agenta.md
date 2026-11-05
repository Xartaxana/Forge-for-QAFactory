# Критик раунда 2 не смог заполнить `scope`/`inputs_read`, а дирижёр не смог вернуть ему форму: S4 встал за шаг до гейта A

id: — | кучка: `hotfix-12586` | от: прогон TP1-12586 на 0.10.5, `testproject1-dev-010`, 29.10.2026 ~13:41, S4; слово владельца 29.10 («ещё один баг фабрики») | приоритет: П1 (0.10.7) | кандидат наверх: нет

## Что наблюдалось

Дирижёр: критик раунда 2 одобрил шесть доработанных кейсов (TC-002, -006, -010, -011, -012 — approve; TC-008 — approve_with_concerns),
но `story_step finish` по `S4-qa-case-critic-2` отказывает: в форме нет строк `scope` и `inputs_read`. Критик записал их в `blocked`:
«the values file accepts only words or flat lists, not lists of objects»; `tried`: «JSON list of objects … refused as nested object»,
«dotted index paths scope.0.id: refused as not path: value». Вернуть форму критику через `SendMessage` нельзя: гард пускает только к
агентам первого раунда. Дирижёр завёл находку проекта `FB-5`.

| Факт | Носитель (стенд, `qa-factory/artifacts/TP1-12586/`) |
|---|---|
| критик раунда 1 заполнил те же списки строками `"scope[0].id": TC-001` — форма это умеет | `work/handoffs/S4-qa-case-critic-1.values.applied.yaml` |
| критик раунда 2: `blocked.tried` — `scope.0.id` и JSON-список | `work/handoffs/S4-qa-case-critic-2.values.applied.yaml` |
| у `S4-qa-case-designer-2` и `S4-qa-case-critic-2` (`purpose: repair_verify`) в записи контроллера `agent_id: None`; у диспатчей раунда 1 он есть | `state/controller.json` |

## Два дефекта

**(а) Отказ не называет форму, которую примет (FR-1, AR-9, AR-10).** `handoff_check.parse_values` знает индексную форму `scope[1].id`,
но называет её только в ветке JSON-ключа; строки «`…` is not a `path: value` line» и «a value is a word or a flat list of words, not a
nested object» и общий совет `FILE_FIX` («write the line as `path: value`…») её не показывают; шапка формы («Fill: write your fields as
"path: value" lines…») тоже. Роль, не видевшая образца, решает, что списки объектов заполнить нельзя, и пишет `blocked`.

**(б) `bind` диспатча доработки не доходит до записи контроллера (AR-22, AR-25).** `story_step bind` пишет `agent_id` через
`stage_done.py` (`pipeline.json`) и квитанцию `state/host-dispatches/`, а гард возврата (`stage_guard.check_resume` →
`_resumable_agents`) верит `agent_id` записи диспатча и стадии `pipeline.json`. У диспатчей `repair_verify` поле в записи пустое —
агенты второго раунда «неизвестны», хотя `bind` их зарегистрировал. Возврат к агенту доработки (единственный дешёвый путь починить форму
без нового диспатча) закрыт.

## Направление

(а) Все три отказа файла значений и шапка формы показывают индексную форму на поле самой формы (`"scope[0].id": <case id>`, по строке
на ключ строки списка); при «nested object» для известного списка формы — готовые строки для первой строки списка. Тест: `scope.0.id` и
JSON-список объектов → отказ называет `scope[0].id`.
(б) `bind` записывает `agent_id` на запись диспатча контроллера для любого `purpose` (тот же писатель, что раунд 1); гард возврата знает
агента доработки. Тест: `rework` → `start` → `bind` → `SendMessage` к этому агенту проходит; к агенту `superseded`-диспатча — отказ, как
сейчас. Сосед: S5/S6 критики кода и раунды автоматора — тот же `bind`.

Принципы и правила: FR-1, FR-2, FR-38, FR-40, P15, P22, AR-9, AR-10, AR-22, AR-25.

Решение владельца нужно: нет (П1 0.10.7 — решение Lead: дефект остановил прогон у гейта A).
