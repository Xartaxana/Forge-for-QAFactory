# Онбординг, установка, хуки и гард — пачка 5: находки, не лежавшие ни в одной пачке

кучка: `onboarding-hooks` | статус: в работе | взял: dev1 (Opus coord), 12.11.2026 | ветка: `pile/onboarding-hooks/batch-5` | MR: — | стенд: частично (живая переустановка, Codex — в live-runs) | приоритет: П2

Собрана 12.11.2026 по слову владельца: находки кучки, не лежавшие ни в одной пачке (разбор t-138). Направления выбраны координатором (Opus, окно lead_degraded) по рекомендациям — до слова владельца/полного Lead любое отменяется.

Правило готовности: пачка закрыта, когда каждый узел «принято» (узлы «ожидает слова владельца» — после слова), свидетели узлов — в журнале взявшего.

Решения владельца: нет (направления выбраны координатором, 12.11.2026; OH5-14 и OH5-15 ждут слова владельца).
очередь: onboarding-hooks/5 → github-move/3
очередь: onboarding-forge/1 → onboarding-hooks/5
очередь: onboarding-forge/3 → onboarding-hooks/5
очередь: onboarding-forge/2 → onboarding-hooks/5
очередь: onboarding-hooks/4 → onboarding-hooks/5
очередь: onboarding-hooks/5 → onboarding-forge/4
очередь: onboarding-hooks/5 → onboarding-hooks/6
очередь: onboarding-hooks/5 → onboarding-hooks/7
Скоуп свидетеля: тестовый файл изменённого модуля и ключи DoD узла; BATCH CANON — интегратор.
Общий бриф дизайнерам: карточка кучки («Дороги», «Содержание»); находка узла; `design/factory-rules.md`; вернуть спеку в `docs/tasks/specs/t-nnn-oh5-n.md`.

## Бриф

Что сделать: разложить 16 находок кучки, не бывших в пачках, по узлам. НЕ делать: узлы других кучек; расширять `publish` (OH5-9); решать вопросы владельца самим (OH5-14, OH5-15).

## Узлы

Исполнитель «designer → builder → critic» — кодовый узел; «builder» — узел-документ или узкая правка. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| OH5-1 | П3 | B-360 (`findings/B-360-zapuskatel-hooks-run-py-cmd-dobavlyaet-k.md`): цена вызова `hooks/run-py.cmd` — сделано узлом speed-cost/1 SC1-5 (кэш интерпретатора, `where` только при промахе кэша, `run-py.cmd:43-62,78-83`); свидетель — тесты SC1-5 | Lead (уже сделано узлом SC1-5) | нет | — | принято (сделано: 47ca1cf6) |
| OH5-2 | П2 | B-142 + B-166 (`findings/B-142-desktop-rezhim-komandy-claude-plugin-root.md`, `findings/B-166-koren-paketa-vo-vremya-raboty-guard-pre-tool-py.md`) — один класс: буквальный `${CLAUDE_PLUGIN_ROOT}` в тексте, который читает роль (`agents/*.md`: qa-retro-analyst:60, qa-failure-analyst:76,78, qa-doc-scribe:63, qa-runner:60; тексты отказов `guard_pre_tool.py` :771..1616; `run_headless.py` не экспортирует переменную). Направление (координатор, по FR-15/FR-37): путь, нужный роли, ДАЁТСЯ ей — тексты отказов подставляют настоящий корень пакета в момент построения (гард знает своё расположение), тела ролей берут путь из брифа (буквальной переменной в теле роли нет), `run_headless` экспортирует то, что дал бы хост. Тест: сканирующий — буквала `${CLAUDE_PLUGIN_ROOT}` нет ни в `agents/*.md`, ни в построенных текстах отказов; текст отказа называет существующий путь | designer → builder → critic | `agents/*.md`, `scripts/guard_pre_tool.py`, `scripts/brief_pack.py` (если бриф несёт корень), `experiments/measurers/run_headless.py`, тесты | — | ожидает |
| OH5-3 | П2 | B-153 (`findings/B-153-progon-bez-sledov-b-003-readiness-py-beret.md`): `readiness.py` берёт `no_trace` только из CLI (:1196, :1208), повторный прогон без флага опрашивает трекер. Направление (находка): `readiness` читает `closed_by_run` задачи, как `gate_preflight`. Тест: задача с `closed_by_run`, без флага — трекер не опрашивается | builder → critic | `scripts/readiness.py`, его тест | — | ожидает |
| OH5-4 | П3 | B-176 (`findings/B-176-posle-t-078-v-artifact-writers-json-poyavilis.md`): четыре читателя реестра (`guard_pre_tool:783`, `artifact_supersede:168`, `contract_slices:347,543`; `story_run` его больше не читает) обязаны видеть ключи-пути `artifact-writers.json`. Направление: табличный тест по читателям со строкой «ключ-путь»; чинится читатель, который её не видит | builder | `scripts/guard_pre_tool.py`, `scripts/artifact_supersede.py`, `scripts/contract_slices.py`, тесты | OH5-2 (`guard_pre_tool.py`) | ожидает |
| OH5-5 | П3 | B-242 (`findings/B-242-zakreplennyy-id-modeli-proveryaetsya-pri-starte.md`): закреплённый id модели не проверяется при старте. Направление (находка): одна строка SessionStart/p0 рядом со строкой версии — печатает, не блокирует. Первый шаг билдера: найти строку версии B-233 и назвать файл. Тест: неизвестный/переименованный id — одна строка, выход 0 | builder | нет заранее: файл строки версии SessionStart назовёт билдер первым шагом (`scripts/tests/` — тест строки) | — | ожидает |
| OH5-6 | П2 | B-249 (`findings/B-249-raskladka-qa-factory-state-propisana-bukvalno-v.md`): `qa-factory/state/...` прописано буквально в 50+ скриптах (host_probe 16, onboard_apply 8, readiness 7, gate_preflight 6, cost_capture 5 и др.). Направление (находка): один носитель раскладки — `install-paths.json` + читатели `runtime_paths`; тест-сторож (shrink-only перепись литерала) | designer → critic на план → builder → critic | `references/install-paths.json`, `scripts/runtime_paths.py`, вызывающие по переписи | onboarding-forge/3 OF3-2 (класс «переносится» в install-paths) и идущие потоки по `hooklib`/`cost_capture` | ожидает |
| OH5-7 | П2 | B-248 (`findings/B-248-pereustanovka-poryadok-proverka-pokrytiya-ubrat.md`): при переустановке устаревший `coverage-map.receipt` даёт REJECT в `check_coverage` раньше retire. Направление (координатор): проверка не читает квитанцию другого поколения пакета (несовпадение подписи — квитанция игнорируется строкой в выводе), порядок шагов не меняется. Тест: проект-фикстура с квитанцией старого поколения — REJECT нет. Живое доказательство переустановки — строка «Живых доказательств» | builder → critic | `scripts/check_coverage.py`, `scripts/onboard_apply.py` (только если нужно), тесты | — | принято: 8f40b43 (t-202) |
| OH5-8 | П2 | B-305 (`findings/B-305-payplayn-7864129-na-kommite-paketa-57b65fb.md`): (а) сделано — `recomputed_word` есть в `scripts/tests/fixtures/driver-layers.json`; (б) тесты на Linux: проверить `test_onboarding_probe.py` и `test_command_proposal.py` на зависимость от `.pytest_cache`, исправить, если есть; (в) живая положительная ветка — строка «Живых доказательств». Тест: оба файла зелёные без `.pytest_cache` | builder | тесты (`scripts/tests/test_onboarding_probe.py`, `scripts/tests/test_command_proposal.py`) | — | ожидает |
| OH5-9 | П3 | B-315 (`findings/B-315-put-publikatsii-baga-iz-kornya-istorii.md`): `publish` разрешает только `task/work` и `task/bugs`, текст роли называет общий `qa-factory/bugs/`. Направление (координатор, узкое): текст называет настоящий путь, который принимает `publish` (`brief_pack.py:167`, `agents/qa-bug-reporter.md`); `publish` не расширяется. Тест: путь из текста — тот, что `publish` принимает | builder | `scripts/brief_pack.py`, `agents/qa-bug-reporter.md`, тест | — | ожидает |
| OH5-10 | П3 | B-325 (`findings/B-325-nativnyy-kontekst-codex-kogda-khost-ne.md`): нативный контекст Codex — несколько пакетов одной роли в ожидании не достаются никому. Направление: сначала измерить (живой `SubagentStart` Codex, идентичность) — строка «Живых доказательств»; починка (срок жизни пакета или явная отмена) выбирается после измерения | builder (после измерения) | `scripts/native_context.py`, тесты | живая строка ниже и onboarding-forge/1 OH3-36 (`native_context.py`) | ожидает |
| OH5-11 | П3 | B-394 (`findings/B-394-u-native-context-pending-path-okolo-stroki-42.md`): `hooklib.artifacts_dir` получает параметр `root`; `native_context.pending_path` (вызывают только тесты) и копия проверки одной компоненты в `worker_lifecycle.py` уходят. Тест: таблица `artifacts_dir(root=...)`; копии не осталось (grep-тест) | builder → critic | `scripts/hooklib.py` (`artifacts_dir`), `scripts/native_context.py`, `scripts/worker_lifecycle.py`, тесты | onboarding-forge/1 OH3-36 и идущий поток по `hooklib` | принято: 00de374 (t-222) |
| OH5-12 | П3 | B-298 (`findings/B-298-klass-put-artefaktov-sobran-ot-proekta-cwd.md`): оставшиеся литеральные места пути артефактов `execution_scheduler.py:154`, `source_exclusions.py:545,568`, `ticket_adapter.py:759` (места `story_run` перепроверить). Направление: читать через единый читатель `artifact_root`, который строит onboarding-forge/3 OF3-1. Тест: те же четыре места читают корень через читателя (таблица случаев) | builder | `scripts/execution_scheduler.py`, `scripts/source_exclusions.py`, `scripts/ticket_adapter.py`, тесты | onboarding-forge/3 OF3-1 | принято: d4ff9a9 (t-252) |
| OH5-13 | П3 | B-451 (`findings/B-451-b-410-identichnost-sessii-ostatki.md`): остатки B-410. F3 (длина пути) — вместе с OH3-36 (onboarding-forge/1), A6 (CLI создают `qa-factory/`) — вместе с OH3-37 (onboarding-forge/1): названы, здесь не делаются. Остальное (две проверки `cd`: `session_identity._cd_target` против `guard_pre_tool._CD_RE` — один выживший; запасной путь через env; прочее) дизайнер разбивает на пункты. F4 (чужая тёплая квитанция помечена `THIS_SESSION`) — ВОПРОС ПОЛНОМУ LEAD: считать ли её этой сессией; до ответа не меняется | designer → builder → critic | `scripts/session_identity.py`, `scripts/guard_pre_tool.py`, тесты | OH5-2 (`guard_pre_tool.py`); OH3-36, OH3-37 (onboarding-forge/1) | ожидает |
| OH5-14 | П3 | B-355 (`findings/B-355-markery-testovykh-putey-references-test-path.md`): добавить ли в `references/test-path-markers.json` `__test__`, `testing`, `integration`, `fixtures`, `_tests`? Вопрос владельцу. Рекомендация: добавить `_tests` и `__test__` (тестовые по имени); `testing`, `integration`, `fixtures` не добавлять — они называют и каталоги продукта. Тест (после слова): таблица маркеров, оба новых имени — тестовый путь, продуктовые `integration/` — нет | builder (после слова) | `references/test-path-markers.json`, тест | слово владельца | ожидает; слово владельца 12.11.2026: добавить пять имён, код — только подсказка, решает роль (запись в находке); идёт новой идеей владельца — разведка t-150 → план владельцу |
| OH5-15 | П3 | B-262 (`findings/B-262-avtoobnovlenie-plagina-vklyuchaetsya-samo-kak-v.md`): автообновление плагина включается фабрикой, если человек его не отключил. Рекомендация: оставить отложенным (владелец отложил 02.10). Решение «делать» — только словом владельца | Lead (после слова владельца) | нет | слово владельца | принято (без правки: держать отложенным — слово владельца 12.11.2026) |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 12.11 — пачка 5 собрана из 16 находок кучки без пачки (t-138, t-140)
- 13.11 — интеграция волны 2 (t-238, ветка `conv/wave-2`): OH5-7 (8f40b43, t-202) влит и принят
- 13.11 t-247/t-255: OH5-7's live-proof expectation is now: live reinstall over a receipt that disagrees with the map — apply completes, regenerate step reports the coverage REJECT, receipt kept (receipt is carried, OH3-9)
- 13.11 — OH5-11 слит в `conv/wave-3` (t-246, интеграция волны 3): merge 00de374 ветки `wip/oh5-11` (t-222, критик t-227)
- 13.11 — OH5-12 слит в `conv/wave-4` (t-261, интеграция волны 4): merge d4ff9a9 ветки `wip/of4-20-oh5-12` (t-252, вместе с OF4-20); OH5-2 часть C слита: merge 597895b ветки `wip/oh5-2c` (t-260); узел OH5-2 остаётся открытым — части A/B не слиты

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|
| OH5-7: живая переустановка со старой `coverage-map.receipt` — REJECT нет, retire выполнен | стенд MyBooks, переустановка | live-runs | перенос: live-runs \| обоснование: живые прогоны не держат пачку \| подтвердил: владелец, 11.11.2026 |
| OH5-8 (в): живая проверка положительной ветки (B-305) | стенд / пайплайн проекта | live-runs | перенос: live-runs \| обоснование: живые прогоны не держат пачку \| подтвердил: владелец, 11.11.2026 |
| OH5-10: измерение идентичности `SubagentStart` на живом Codex (B-325) | Codex, живой хост | live-runs | перенос: live-runs \| обоснование: живые прогоны не держат пачку \| подтвердил: владелец, 11.11.2026 |

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->
