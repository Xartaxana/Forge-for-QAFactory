# Бриф S5 автоматора не несёт строк об учётках стенда: `manual_stand_lines` зовётся только для ручного блока, а текст роли ссылается на «строку брифа» (t-561 Ф-9 b, Ф-13)

id: — | кучка: `execution-report` | от: критик t-561, Ф-9 (б) и Ф-13 (`docs/tasks/specs/reviews/t-561-s4-critic.md`), п. 3 находки «S5 у автоматора строки нет», 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

- `brief_pack.py:2611–2615`: раздел `## The stand` (`manual_stand_lines`, :2368) строится только при `_record_kind(dispatch) == "manual"`. Бриф автоматора S5 (`qa-automator`, диспатч `plan`/`code`) строки о том, какие аккаунты есть и у каких ролей учётки нет
  (`_unpaired_actor_lines`, :2284: «role X has no recorded account. Do not sign in as another account in its place»), не получает. Читатель без производителя (AR-22): `agents/qa-automator.md` называет «the brief says a role has no recorded account» —
  критик Ф-13 потребовал убрать скобку из текста роли, а строку на бриф S5 завести узлом здесь; ручной бриф верен. t-506 7.2 п. 4 просил S5 и S6.
- Следствие: автоматор пишет тест, входящий под чужой ролью или с придуманным аккаунтом (P20), потому что бриф про учётки молчит; проверка роли/аккаунта живёт только в ручной ветке.

## Что именно менять

1. `brief_pack.py`: новая `automator_account_lines(task_root, project, cfg, scope, env_name) -> list` — подмножество `manual_stand_lines`: `- Accounts: …` (имена ролей, `credentials_by_role`; значения не печатаются), `- Env keys:` (имена ключей через `_env_file_key_names`) и `- Case actors:`
   с `role "X" has no recorded account` (`_case_actor_lines`, `_unpaired_actor_lines`). Общие части — те же функции, не копии (AR-13, AR-15): `manual_stand_lines` вызывает её для общей части.
2. Место вызова (:2611): `if _record_kind(dispatch) == "manual": stand = manual_stand_lines(…)` дополняется `elif stage == "S5" and role == "qa-automator": stand = automator_account_lines(…)`; рендер раздела (`render`, :2629 `if stand:`) не меняется. Лимиты: `STAND_CASE_LINES_MAX` как у ручного, остаток «(+N more)» (край назван).
3. `agents/qa-automator.md`: фраза про «the brief says a role has no recorded account» остаётся ТОЛЬКО если п. 1–2 выполнены в том же коммите (иначе скобка убирается). Размер роли — под лимитом A25.
4. Тесты (`scripts/tests/test_brief_pack_manual.py` по образцу K7:456–467 и новый S5-случай): бриф S5 автоматора с ролью без пары содержит строку `has no recorded account`; без акторов — строки нет; значений ключей в брифе нет; бриф автоматического блока ручной ветки не меняется. Мутация: не вызывать `automator_account_lines` — красит первый.

## Принципы и правила

P5, P20, P14; FR-11, FR-38, FR-49; AR-8, AR-10, AR-21, AR-22. Связи: OH3-40, EP1-31, `findings/20261031-dva-razbora-env-fajla.md`.

Решение владельца нужно: нет.
