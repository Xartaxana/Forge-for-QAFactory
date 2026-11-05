# Предупреждения S0 `host_hooks unknown; vcs_api unknown`, `live parity: not_certified` висят до конца прогона

id: — | кучка: `onboarding-forge` | от: прогон CART-1 (MyBooks), 31.10.2026 | приоритет: П2 | кандидат наверх: нет

## Что наблюдалось

Свод п. 7.10 (мелочь); отчёт `docs/tasks/specs/reports/t-1633-cart1-run-problems-transcript.md`, строка 2 (S0, 00:16:10 UTC, L90–L96): готовность показала
«host_integration observed_partial missing: exit_gate.py, host_dispatch.py, inject_context.py … live parity: not_certified», «host_hooks unknown», «vcs_api unknown»;
дирижёр записал их в `pipeline.json.warnings` (L96) и пошёл дальше; до гейта B (12:12 UTC) они не разрешились. Потеря времени ≈ 0; потеря — шум, который каждую историю читает дирижёр и человек.
В отчёте причина названа «не проверял».

Прочитано 31.10.2026 (это причина):
- `scripts/host_capabilities.py` `inspect()` (`:53`–`:97`): `missing` — скрипты, от которых ещё нет файла-расписки хука в `qa-factory/state/host-receipts/`; на свежем проекте и на S0 первой истории список длинный по построению — это счёт не дефекта, а ещё не случившихся вызовов. `live_parity` = `essential_verified` только при `story_ready` (живая проба `host_probe.py --check` пройдена), иначе `not_certified`.
- `host_hooks` = `unknown` до тех пор, пока кто-то не прогонит живую пробу (пара команд `host_probe.py --prepare` / `--check`, `qa-doctor` шаг 1b; `readiness.py:996`–`:1006`: `remedy.autorun False`, `blocks: nothing on its own`); `vcs_api` = `unknown` без `readiness.py --probe-vcs` (`:990`–`:992`).
- `readiness.py --require` (`:1117`–`:1121`): `unknown` — не блокер, «the gap is named at gate A»; строка печатается как `WARN` каждый раз.
- Не проверено: кто и по какому шагу пишет эти строки в `pipeline.json.warnings` (искать в `skills/qa-story/phases/s0.md` и `story_step`); нужна ли истории вообще проба хуков (профиль `web`, host_hooks нужен гарду ролей, vcs_api — только если истории нужен MR).

Связь: `qa-doctor/SKILL.md:245` («`vcs_api`/`host_hooks` are never the next action unless an open story needs them») — то же решение для другого входа.

## Класс

Неизвестное окружение хоста печатается как предупреждение при каждом запуске и никогда не разрешается и не отбрасывается как «этой истории не нужно» (FR-41: неизвестное не выдаётся за факт; AR-28: неизвестное не становится проходом — но и не висит вечно без хода). Не проект: любой проект в первой истории.

## Что именно менять

Направление выбрано: предупреждение несёт ход (нужно ли это истории) и не повторяет счёт недостающих расписок на S0.
1. `scripts/readiness.py` `print_summary` (`:1056`): строка `host_integration` не печатает `missing: …` пока `observed` пуст или `story_ready` ложно из-за непроверенной пробы; вместо списка — «receipts so far: N of 10 expected scripts (they accumulate as the story runs)». Тест `scripts/tests/test_readiness.py`: свежий проект → в выводе нет `missing:` и есть `receipts so far: 0 of 10`; проект со всеми расписками → без изменений.
2. `readiness.py --require` (`:1121`): для `unknown`-возможности, которой нет в `--require`, предупреждение заменяется одной строкой `NOTE <name>: unknown; this story did not ask for it` (то, что истории не нужно, не шумит); для запрошенной — `WARN` как сейчас и ход (команда пробы из `remedy`, `readiness.py:1002`). Тест: `--require vcs_api` на проекте без пробы → `WARN`; без `--require` → `NOTE`, не `WARN`.
3. Что пишет дирижёр в `pipeline.json.warnings` — после пункта 2 строки `NOTE` не копируются (место копирования найти первым шагом; не проверено).

Принципы и правила: P1, P9, P11, FR-4, FR-41, AR-12, AR-28.

Решение владельца нужно: нет.
