# Мутационная проба критика кода не запускается при двух профилях на общем корне тестов: `probe_by_code.build_request` не передаёт `profile_id`

id: — | кучка: `execution-probes` | от: Lead-сессия (Opus, окно `lead_degraded`), 24.10.2026, по прогону TP1-12586 на testproject1-dev-010 | приоритет: П1 | кандидат наверх: нет

перенос: hotfix-12586/batch-2 (узел HF2-8 (EP1-16), волна 1; слово владельца 25.10.2026 — срочная пачка; узел здесь закрывается её хэшем)

Слово владельца 24.10.2026: «ещё один дефект фабрики: S5 window 1 is written and statically reviewed clean … The critic's mutation probe cannot
run because of a factory defect».

## Что было (скаут t-1220, `docs/tasks/handoffs/t-1220-s5-mutation-probe-defect-recon.md`)

Все пять проб окна 1 (`work/probes/*.json`) — `verdict: not_executed`, тест не запускался. Отказ (20:36 и 21:15 UTC):
«MineRefusal: profiles api, ui share the test root `testproject1_test_harness/tests` … name it on the manifest row (`profile_id`) or with --profile ID».
Красные по требованию TC-004/TC-009 не причина: тот же отказ у зелёного generic-теста.

## Причина

`scripts/probe_by_code.py` (`build_request`, ~1317-1327): `profile_id` строки манифеста используется для `--cwd` (`_profile_cwd`), но в
`build_mine_request` не передаётся; для проб по `node_ids` `execution_request.build_mine_request` собирает строку с пустым entry, и `_profile_for`
отказывает «два профиля на общем корне» (HF1-3/EP1-10, 7878f388 сделал выбор профиля явным — тихий первый профиль закрыт, путь `node_ids` пробы —
нет; сверено Lead по коду). Отказ называет дверь `--profile`, которой у пробы нет (`probe_by_code.py:1159`: «This tool takes no `--profile`») — FR-2.

## Что сделал дирижёр

FB-4 в бэклог стенда; по слову человека «tests may stay unprobed in all S5 windows; S8 lists them under Left with you» — девять `human_answer`
(дверь HF1-14 `window_record.probe_gap_block`). Не потеряно, но S8 этого прогона ещё не писал — проверить, что «Left with you» назовёт пять проб.

## Что сделать (форма)

- `build_request` передаёт `profile_id` строки в `build_mine_request`; ветка `node_ids` сохраняет entry/`profile_id`.
- Тест: два профиля на общем корне + строка манифеста с `profile_id` → проба строится и запускается; без `profile_id` — отказ с дверью, которая у
  пробы есть (строка манифеста), без `--profile`.
- Соседи по карте: `probe_by_code.py` (`_profile_cwd` уже читает `entry_profile_id`), `red_sandbox`, `run_suite --mine` — тот же вызов
  `build_mine_request` без профиля.
- Живое доказательство: проба красного по требованию теста после починки (не проверялась ни разу).

Связи: EP1-10 / HF1-3 (один предикат владельца профиля), HF1-14 (дверь «проба не запускалась»), TQ1-5 (проба мутирует только первый assert),
GW1-22 (не тот класс). Принципы и правила: FR-2, FR-17, FR-18, FR-41, AR-9, AR-13, AR-15.

Решение владельца нужно: нет.
